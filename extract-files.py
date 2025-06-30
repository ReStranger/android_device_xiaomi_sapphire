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
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sapphire',
    'hardware/qcom-caf/sm6225',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs): # fmt: skip
    return f'{lib}_{partition}' if partition == 'vendor' else None # fmt: skip


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
    ): lib_fixup_vendor_suffix,
    (
        'libagm',
        'libar-acdb',
        'libar-gpr',
        'libar-gsl',
        'libar-pal',
        'libats',
        'liblx-osal',
        'libpalclient',
        'audio.primary.bengal',
    ): lib_fixup_remove,
}
blob_fixups: blob_fixups_user_type = {
    ('vendor/bin/hw/android.hardware.security.keymint-service-qti', 'vendor/lib64/libqtikeymint.so'): blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
     'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    'vendor/etc/init/android.hardware.gnss-aidl-service-qti.rc': blob_fixup()
        .regex_replace('group system gps radio vendor_qti_diag vendor_ssgtzd', 'group system gps radio vendor_qti_diag'),
    ('vendor/bin/STFlashTool', 'vendor/lib64/libstfactory-vendor.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    (
        'vendor/lib64/libalLDC.so',
        'vendor/lib64/libalhLDC.so',
        'vendor/lib64/libmorpho_ldc.so',
        'vendor/lib64/libmorpho_Ldc.so',
        'vendor/lib64/libmorpho_ubwc.so',
        'vendor/lib64/libTrueSight.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_acquire')
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/etc/vintf/manifest/c2_manifest_vendor.xml': blob_fixup()
        .regex_replace('.+DOLBY.+\n', ''),
    ('vendor/etc/media_codecs.xml', 'media_codecs_khaje_iot.xml', 'media_codecs_khaje_v0.xml'): blob_fixup()
        .regex_replace('.+media_codecs_(google_audio|google_c2|google_telephony|vendor_audio).+\n', ''),
}  # fmt: skip

module = ExtractUtilsModule(
    'sapphire',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if (__name__ == '__main__'): # fmt: skip
    utils = ExtractUtils.device(module) # fmt: skip
    utils.run()
