#pragma once

#include <smacc2/smacc.hpp>
#include <smacc2/client_bases/smacc_service_client.hpp>

#include <lifecycle_msgs/srv/change_state.hpp>

#include <amp_sm/clients/cl_topic_listener.hpp>
#include <amp_sm/clients/cl_lifecycle_monitor.hpp>
#include <amp_sm/clients/cl_lifecycle_pipeline.hpp>

namespace amp_sm
{
class or_check : public smacc2::Orthogonal<or_check>
{
public:
    void onInitialize() override
    {   
        this->createClient<amp_sm::ClCheckLifecycle>();

        this->createClient<
            smacc2::client_bases::SmaccServiceClient<lifecycle_msgs::srv::ChangeState>
        >("/float_publisher/change_state");

        this->createClient<amp_sm::ClLifecycleMonitor>(std::vector<std::string>{
            "/float_publisher"
            //...
        });

        this->createClient<amp_sm::ClLifecycleConsensusMonitor>(std::vector<std::string>{
            "/float_publisher"
            //...
        });

        this->createClient<amp_sm::ClMissionSelectListener>();
        this->createClient<amp_sm::ClGoListener>();
        this->createClient<amp_sm::ClFinishedListener>();
    }
};
} // namespace amp_sm