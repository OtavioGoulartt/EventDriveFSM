#pragma once

#include <smacc2/client_bases/smacc_service_client.hpp>
#include <lifecycle_msgs/srv/change_state.hpp>
#include <string>
#include <memory>

namespace amp_sm
{
/**
 * @brief Classe Base (Mãe) de Lifecycle para os nós gerenciados do veículo.
 * Fornece a funcionalidade de enviar comandos assíncronos (Fire and Forget)
 * sem travar a thread da máquina de estados.
 */
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
} // namespace amp_sm