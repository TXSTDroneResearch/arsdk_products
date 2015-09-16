###############################################################################
## @file product.mk
##
##
## Product common alchemy variables.
###############################################################################

# Product common config dir
COMMON_CONFIG_ANDROID_DIR := $(call my-dir)

include $(COMMON_CONFIG_ANDROID_DIR)/../common.mk

TARGET_OS = linux
TARGET_OS_FLAVOUR = android
TARGET_LIBC = bionic
#export TARGET_CPU = p6i

TARGET_ANDROID_APILEVEL = 14
TARGET_ANDROID_NDK = $(ANDROID_NDK_PATH)
TARGET_ANDROID_SDK = $(ANDROID_SDK_PATH)

TARGET_DEFAULT_LIB_DESTDIR="usr/lib"
