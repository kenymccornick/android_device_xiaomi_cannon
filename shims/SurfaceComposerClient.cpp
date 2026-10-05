#include <gui/SurfaceComposerClient.h>

__attribute__((visibility("default"), used))
android::sp<android::IBinder> getInternalDisplayTokenShim()
    __asm__("_ZN7android21SurfaceComposerClient23getInternalDisplayTokenEv");

android::sp<android::IBinder> getInternalDisplayTokenShim()
{
    const auto displayIds =
            android::SurfaceComposerClient::getPhysicalDisplayIds();

    if (displayIds.empty())
        return nullptr;

    return android::SurfaceComposerClient::getPhysicalDisplayToken(displayIds.front());
}
