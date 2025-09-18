// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from doom_interfaces:msg/CentroidCoords.idl
// generated code does not contain a copyright notice
#ifndef DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "doom_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "doom_interfaces/msg/detail/centroid_coords__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
bool cdr_serialize_doom_interfaces__msg__CentroidCoords(
  const doom_interfaces__msg__CentroidCoords * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
bool cdr_deserialize_doom_interfaces__msg__CentroidCoords(
  eprosima::fastcdr::Cdr &,
  doom_interfaces__msg__CentroidCoords * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
size_t get_serialized_size_doom_interfaces__msg__CentroidCoords(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
size_t max_serialized_size_doom_interfaces__msg__CentroidCoords(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
bool cdr_serialize_key_doom_interfaces__msg__CentroidCoords(
  const doom_interfaces__msg__CentroidCoords * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
size_t get_serialized_size_key_doom_interfaces__msg__CentroidCoords(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
size_t max_serialized_size_key_doom_interfaces__msg__CentroidCoords(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_doom_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, doom_interfaces, msg, CentroidCoords)();

#ifdef __cplusplus
}
#endif

#endif  // DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
