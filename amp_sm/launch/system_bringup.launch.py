import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # ========================================================================
    # 2. Criar os comandos de inclusão (chamar os ficheiros .launch.py)
    # ========================================================================
    
    repeater_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('amp_sm'), 'launch', 'repeater_lifecycle.launch.py')
        )
    )

    check_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('control'), 'launch', 'check_lifecycle.launch.py')
        )
    )

    # ========================================================================
    # 3. Retornar a lista de ficheiros para o ROS 2 executar
    # ========================================================================
    return LaunchDescription([
        LogInfo(msg="=== INICIANDO O BRINGUP DO SISTEMA AMPERA ==="),
        repeater_launch,
        check_launch
        ])