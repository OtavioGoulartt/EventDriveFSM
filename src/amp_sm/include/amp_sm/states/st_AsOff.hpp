#pragma once

#include <smacc2/smacc.hpp>
#include <lifecycle_msgs/msg/transition.hpp>

#include "../client_behaviors/cb_change_lifecycle.hpp"
#include <amp_sm/clients/cl_lifecycle_pipeline.hpp>
#include <amp_sm/clients/cl_topic_listener.hpp>
namespace amp_sm
{
struct st_AsSetup;

struct st_off : smacc2::SmaccState<st_off, Amp_sm>
{
    using SmaccState::SmaccState;

    typedef boost::mpl::list<
        smacc2::Transition<amp_sm::EvSaltoAutomatico, amp_sm::st_AsSetup>  
    > reactions;

    static void staticConfigure()
    {
        //
    }

    void onEntry()
    {
        RCLCPP_INFO(getLogger(), "Estado off: Disparando comandos de configuração...");
        this->postEvent<EvSaltoAutomatico>();
    }

    void onExit()
    {
        RCLCPP_INFO(getLogger(), "Estado off: Saltando automaticamente para st_AsSetup!");
    }
};
} // namespace amp_sm