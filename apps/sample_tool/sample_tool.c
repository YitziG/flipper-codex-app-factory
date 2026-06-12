#include <furi.h>

#define TAG "sample_tool"

int32_t sample_tool_app(void* p) {
    UNUSED(p);
    FURI_LOG_I(TAG, "Sample Tool started");
    return 0;
}
