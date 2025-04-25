#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3

#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixup_remove_arch_suffix,
    lib_fixup_vendorcompat,
    lib_fixup_remove,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
    libs_proto_3_9_1,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/cannon',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]

lib_fixups: lib_fixups_user_type = {
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    ('libsink',): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'system/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService'),

    'system/priv-app/LPPeService/LPPeService.apk': blob_fixup()
        .apktool_patch('blob-patches/LPPeService'),

    'system/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),

    'system/lib64/libsink.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),

    (
        'system/lib/libem_support_jni.so',
        'system/lib64/libem_support_jni.so',
    ): blob_fixup()
        .add_needed('libgui_cannon_shim.so'),

    'vendor/bin/hw/android.hardware.thermal@2.0-service.mtk': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),

    'vendor/bin/hw/camerahalserver': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),

    (
        'vendor/lib/hw/vendor.mediatek.hardware.pq@2.13-impl.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.13-impl.so',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),

    (
        'vendor/bin/mnld',
        'vendor/lib/libaalservice.so',
        'vendor/lib64/libaalservice.so',
        'vendor/lib/librgbwlightsensor.so',
        'vendor/lib64/librgbwlightsensor.so',
        'vendor/lib64/libcam.utils.sensorprovider.so',
    ): blob_fixup()
        .replace_needed(
            'libsensorndkbridge.so',
            'android.hardware.sensors@1.0-convert-shared.so',
        ),

    (
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek',
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b',
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed(
            'libavservices_minijail_vendor.so',
            'libavservices_minijail.so',
        ),
        
    'vendor/lib64/libmtkcam_featurepolicy.so': blob_fixup()
        .binary_regex_replace(
            b'\xE8\x87\x40\xB9',
            b'\x28\x02\x80\x52',
        ),

    (
        'vendor/lib64/libteei_daemon_vfs.so',
        'vendor/lib64/lib3a.flash.so',
        'vendor/lib64/libaaa_ltm.so',
        'vendor/lib64/lib3a.ae.stat.so',
        'vendor/lib64/lib3a.sensors.color.so',
        'vendor/lib64/lib3a.sensors.flicker.so',
        'vendor/lib64/libSQLiteModule_VER_ALL.so',
    ): blob_fixup()
         .add_needed('liblog.so'),

    'vendor/lib64/libmnl.so' : blob_fixup()
         .add_needed('libcutils.so'),
         
    'vendor/lib64/libvidhance.so': blob_fixup()
        .add_needed('libcomparetf2_shim.so')
        .add_needed('libdemangle.so')
        
    (
        'vendor/lib/libnvram.so',
        'vendor/lib64/libnvram.so',
        'vendor/lib64/libsysenv.so',
        'vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron',
        'vendor/lib/nfc_nci.nqx.default.hw.so',
        'vendor/lib64/nfc_nci.nqx.default.hw.so',
    ) : blob_fixup()
         .add_needed('libbase_shim.so'),

    (
        'vendor/bin/hw/android.hardware.gnss-service.mediatek',
        'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed(
            'android.hardware.gnss-V1-ndk_platform.so',
            'android.hardware.gnss-V1-ndk.so',
        ),
         
}  # fmt: skip

module = ExtractUtilsModule(
    'cannon',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
