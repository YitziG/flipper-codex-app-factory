#include <furi.h>

#define TAG "{{APPID}}"

int32_t {{APPID}}_app(void* p) {
    UNUSED(p);
    FURI_LOG_I(TAG, "{{NAME}} started");
    return 0;
}
