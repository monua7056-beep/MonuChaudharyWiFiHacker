[app]
title = Monu Chaudhary WiFi Hacker
package.name = monuwifi
package.domain = com.monuchaudhary
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0
requirements = python3,kivy==2.2.0
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,NEARBY_WIFI_DEVICES,INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 1
