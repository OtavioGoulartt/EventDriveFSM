#pragma once

#include <smacc2/smacc.hpp>
#include <lifecycle_msgs/msg/transition.hpp>

#include "../client_behaviors/cb_change_lifecycle.hpp"
#include <amp_sm/clients/cl_lifecycle_pipeline.hpp>
#include <amp_sm/clients/cl_topic_listener.hpp>

namespace amp_sm
{
struct st_AsReady;

struct st_AsSetup : smacc2::SmaccState<st_AsSetup, Amp_sm>
{
    using SmaccState::SmaccState;

    typedef boost::mpl::list<
    smacc2::Transition<amp_sm::EvAllNodesConfigured, amp_sm::st_AsReady>
    > reactions;

    static void staticConfigure() // configurar todos os lifecycles necessarios.
    {
        configure_orthogonal<or_check, CbChangeLifecycle<ClCheckLifecycle>>(
            lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE
            );

    }
    
    void onEntry()
    {
        RCLCPP_INFO(getLogger(), "Estado setup: Verificando o sistema...");
    }
};
} // namespace amp_sm