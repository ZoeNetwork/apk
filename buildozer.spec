[app]

title = Zoe MMDVM Hotspot
package.name = zoemmdvmhotspot
package.domain = org.example
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,requests
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1
