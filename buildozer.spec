[app]
title = Monu Chaudhary WiFi Hacker
package.name = monuwifi
package.domain = com.monuchaudhary
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,ACCESS_FINE_LOCATION,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,NEARBY_WIFI_DEVICES,INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 1
