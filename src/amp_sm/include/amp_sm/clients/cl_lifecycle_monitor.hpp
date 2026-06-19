#pragma once

#include <map>
#include <string>
#include <vector>

#include <smacc2/smacc_client.hpp>
#include <lifecycle_msgs/msg/transition_event.hpp>

namespace amp_sm
{

struct EvNodeActivated   : boost::statechart::event<EvNodeActivated> {};
struct EvNodeDeactivated : boost::statechart::event<EvNodeDeactivated> {};
struct EvNodeCrashed     : boost::statechart::event<EvNodeCrashed> {};

struct EvAllNodesConfigured : boost::statechart::event<EvAllNodesConfigured> {};
struct EvAllNodesActivated  : boost::statechart::event<EvAllNodesActivated> {};

class ClLifecycleMonitor : public smacc2::ISmaccClient
{
public:
    ClLifecycleMonitor(const std::vector<std::string> & target_nodes)
    : node_names_(target_nodes)
    {
    }

    void onInitialize() override
    {
        for (const std::string & name : node_names_)
        {
            std::string topic_name = name + "/transition_event";

            auto sub = getNode()->create_subscription<lifecycle_msgs::msg::TransitionEvent>(
                topic_name, 10,
                [this, name](const lifecycle_msgs::msg::TransitionEvent::SharedPtr msg) {
                    this->messageCallback(msg, name);
                }
            );
            subs_.push_back(sub);
        }
    }

private:
    std::vector<std::string> node_names_;
    std::vector<rclcpp::Subscription<lifecycle_msgs::msg::TransitionEvent>::SharedPtr> subs_;

    void messageCallback(const lifecycle_msgs::msg::TransitionEvent::SharedPtr msg, const std::string & node_name)
    {
        std::string novo_estado = msg->goal_state.label;

        RCLCPP_INFO(getLogger(), "[Monitor Individual -> %s] mudou para o estado: %s", 
                    node_name.c_str(), novo_estado.c_str());

        if (novo_estado == "active")
        {
            this->postEvent<EvNodeActivated>();
        }
        else if (novo_estado == "inactive")
        {
            this->postEvent<EvNodeDeactivated>();
        }
        else if (novo_estado == "unconfigured" || novo_estado == "errorprocessing")
        {
            RCLCPP_ERROR(getLogger(), "[Monitor Individual -> %s] ALERTA CRITICO!", node_name.c_str());
            this->postEvent<EvNodeCrashed>();
        }
    }
};

class ClLifecycleConsensusMonitor : public smacc2::ISmaccClient
{
public:
    ClLifecycleConsensusMonitor(const std::vector<std::string> & target_nodes)
    : node_names_(target_nodes)
    {
    }

    void onInitialize() override
    {
        for (const std::string & name : node_names_)
        {
            node_states_[name] = "unknown";

            std::string topic_name = name + "/transition_event";
            auto sub = getNode()->create_subscription<lifecycle_msgs::msg::TransitionEvent>(
                topic_name, 10,
                [this, name](const lifecycle_msgs::msg::TransitionEvent::SharedPtr msg) {
                    this->messageCallback(msg, name);
                }
            );
            subs_.push_back(sub);
        }
    }

private:
    std::vector<std::string> node_names_;
    std::vector<rclcpp::Subscription<lifecycle_msgs::msg::TransitionEvent>::SharedPtr> subs_;
    std::map<std::string, std::string> node_states_;

    void messageCallback(const lifecycle_msgs::msg::TransitionEvent::SharedPtr msg, const std::string & node_name)
    {
        std::string novo_estado = msg->goal_state.label;
        
        node_states_[node_name] = novo_estado;

        RCLCPP_INFO(getLogger(), "[Consenso -> %s] reportou estado: %s", node_name.c_str(), novo_estado.c_str());

        if (novo_estado == "errorprocessing" || novo_estado == "finalized")
        {
            RCLCPP_ERROR(getLogger(), " [Consenso] O no %s falhou! Abortando operacao em grupo.", node_name.c_str());
            this->postEvent<EvNodeCrashed>();
            return;
        }

        checkConsensus();
    }

    void checkConsensus()
    {
        bool all_configured = true;
        bool all_activated = true;

        for (const auto & pair : node_states_)
        {
            if (pair.second != "inactive") all_configured = false;
            if (pair.second != "active") all_activated = false;
        }

        if (all_configured)
        {
            RCLCPP_INFO(getLogger(), " [Consenso] SUCESSO! Todos os nos estao CONFIGURADOS na memoria.");
            this->postEvent<EvAllNodesConfigured>();
        }
        
        if (all_activated)
        {
            RCLCPP_INFO(getLogger(), " [Consenso] SUCESSO! Todos os nos estao ATIVADOS a 100%%.");
            this->postEvent<EvAllNodesActivated>();
        }
    }
};

}