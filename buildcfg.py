
import sys, os
import dragon

# Disable all default tasks and import arsdk ones
keep_list = [
    "alchemy",
    "geneclipse",
    "publish",
    "reference-checker",
    "reference-creator",
]
dragon.disable_def_tasks(keep_list=keep_list)
from arsdktasks import *

android_samples_dir = os.path.join(dragon.WORKSPACE_DIR,
        "packages", "Samples", "Android")

ios_samples_dir = os.path.join(dragon.WORKSPACE_DIR,
        "packages", "Samples", "iOS")

#===============================================================================
# Android
#===============================================================================
def build_android_jni(dirpath, args):
    dragon.exec_dir_cmd(dirpath=dirpath, cmd="${ANDROID_NDK_PATH}/ndk-build")

def build_android_app(dirpath, args, release=False):
    # Build application
    cmd = "./gradlew "
    cmd += "assembleRelease " if release else "assembleDebug "
    if args:
        cmd += " ".join(args)
    dragon.exec_dir_cmd(dirpath=dirpath, cmd=cmd)

def add_android_sample(sample):
    dragon.add_meta_task(
        name = "build-jni-%s" % sample,
        desc = "Build android sdk & jni for %s" % sample,
        subtasks = ["build-sdk"],
        posthook = lambda task, args: build_android_jni(
                os.path.join(android_samples_dir, sample, "app", "jni"),
                args)
        )

    dragon.add_meta_task(
        name = "build-sample-%s" % sample,
        desc = "Build android sdk & jni & sample for %s" % sample,
        subtasks = ["build-jni-%s" % sample],
        posthook = lambda task, args: build_android_app(
                os.path.join(android_samples_dir, sample),
                args, release=False)
        )

if dragon.VARIANT == "android":
    all_samples = []
    if os.path.exists(android_samples_dir):
        for sample in os.listdir(android_samples_dir):
            add_android_sample(sample)
            all_samples.append("build-sample-%s" % sample)

        dragon.add_meta_task(
            name = "build-samples",
            desc = "Build all android samples",
            subtasks = all_samples
    )

#===============================================================================
# iOS
#===============================================================================
def build_ios_app(dirpath, project, sdk, args, release=False):
    # Build application
    cmd = "xcodebuild "
    cmd += "-project %s " % project
    cmd += "-sdk %s " % sdk
    if sdk == "iphonesimulator":
        cmd += "-arch x86_64 "
    cmd += "-configuration Release " if release else "-configuration Debug "
    if args:
        cmd += " ".join(args)
    dragon.exec_dir_cmd(dirpath=dirpath, cmd=cmd)

def add_ios_sample(sample):
    dragon.add_meta_task(
        name = "build-sample-%s" % sample,
        desc = "Build ios sdk & sample for %s" % sample,
        subtasks = ["build-sdk"],
        posthook = lambda task, args: build_ios_app(
               os.path.join(ios_samples_dir, sample, sample),
               sample + ".xcodeproj",
               "iphoneos" if dragon.VARIANT == "ios" else "iphonesimulator",
               args, release=False)
        )

if dragon.VARIANT == "ios" or dragon.VARIANT == "ios_sim":
    all_samples = []
    if os.path.exists(android_samples_dir):
        for sample in os.listdir(ios_samples_dir):
            add_ios_sample(sample)
            all_samples.append("build-sample-%s" % sample)

        dragon.add_meta_task(
            name = "build-samples",
            desc = "Build all android samples",
            subtasks = all_samples
    )

#===============================================================================
# Unix
#===============================================================================

def add_unix_sample(sample):
    dragon.add_alchemy_task(
        name = "build-sample-%s" % sample,
        desc = "Build unix sdk sample for %s" % sample,
        product = dragon.PRODUCT,
        variant = dragon.VARIANT,
        defargs = [sample],
    )

if dragon.VARIANT == "native":
    all_samples = []
    samples = ["BebopDroneDecodeStream", "BebopDroneReceiveStream",
               "BebopPilotingNewAPI", "JumpingSumoPilotingNewAPI",
               "JumpingSumoChangePosture", "JumpingSumoPiloting",
               "JumpingSumoReceiveStream"]
    for sample in samples:
        add_unix_sample(sample)
        all_samples.append("build-sample-%s" % sample)

    dragon.add_meta_task(
        name = "build-samples",
        desc = "Build all native samples",
        subtasks = all_samples
    )

#===============================================================================
# generate sources task
#===============================================================================
def hook_gen_sources(task, args):
    packages_dir = os.path.join(dragon.WORKSPACE_DIR, "packages")
    for package in os.listdir(packages_dir):
        try:
            path = os.path.join(packages_dir, package)
            if os.path.isfile(os.path.join(path, "updateGenerated.sh")):
                dragon.exec_dir_cmd(dirpath=path, cmd="./updateGenerated.sh")
                dragon.exec_dir_cmd(dirpath=path, cmd="git status")
        except dragon.TaskError as ex:
            dragon.logging.error(str(ex))

dragon.add_meta_task(
    name = "gensources",
    desc = "Generate all sdk sources",
    posthook = hook_gen_sources,
)
