#pragma once

#include <amp_sm/clients/cl_lifecycle_interface.hpp>

namespace amp_sm
{
/**
 * @brief Cliente focado no ciclo de vida do subsistema de Check.
 */
class ClCheckLifecycle : public ClLifecycleInterface
{
public:
    // 2. Fica minúsculo: apenas repassa a string de destino para a classe mãe
    ClCheckLifecycle() 
        : ClLifecycleInterface("/float_publisher/change_state")
    {
    }
};
} // namespace amp_sm

