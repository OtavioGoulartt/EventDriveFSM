#pragma once

#include <smacc2/smacc_client.hpp>
#include <lifecycle_msgs/srv/change_state.hpp>
#include <map>
#include <string>
#include <vector>
#include <memory>
#include <smacc2/client_bases/smacc_service_client.hpp>


namespace amp_sm
{

class ClLifecycleInterface : public smacc2::client_bases::SmaccServiceClient<lifecycle_msgs::srv::ChangeState>
{
public:
    // O construtor recebe o nome do serviço do nó e repassa para o SMACC2
    ClLifecycleInterface(std::string service_name) 
        : smacc2::client_bases::SmaccServiceClient<lifecycle_msgs::srv::ChangeState>(service_name)
    {
    }

    // A PORTA PÚBLICA: Pega o pedido do Behavior e envia para a rede ROS 2 de forma assíncrona
    void async_change_state(std::shared_ptr<lifecycle_msgs::srv::ChangeState::Request> request)
    {
        if (this->client_ != nullptr)
        {
            // async_send_request não trava a Thread, resolvendo o problema do Deadlock!
            this->client_->async_send_request(request);
        }
        else
        {
            RCLCPP_ERROR(getLogger(), "[ClLifecycleInterface] Falha Crítica: client_ ROS 2 não inicializado!");
        }
    }
};

/**
 * @brief Cliente focado no ciclo de vida do subsistema de Check.
 */
class ClCheckLifecycle : public ClLifecycleInterface
{
public:
    // 2. Fica minúsculo: apenas repassa a string de destino para a classe mãe
    ClCheckLifecycle() 
        : ClLifecycleInterface("/check_node_lifecycle/change_state")
    {
    }
};
class ClRepeaterLifecycle : public ClLifecycleInterface
{
public:
    // 2. Fica minúsculo: apenas repassa a string de destino para a classe mãe
    ClRepeaterLifecycle() 
        : ClLifecycleInterface("/repeater_node/change_state")
    {
    }
};

} // namespace amp_sm

