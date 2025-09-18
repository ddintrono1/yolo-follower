// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from doom_interfaces:msg/CentroidCoords.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "doom_interfaces/msg/detail/centroid_coords__rosidl_typesupport_introspection_c.h"
#include "doom_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "doom_interfaces/msg/detail/centroid_coords__functions.h"
#include "doom_interfaces/msg/detail/centroid_coords__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  doom_interfaces__msg__CentroidCoords__init(message_memory);
}

void doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_fini_function(void * message_memory)
{
  doom_interfaces__msg__CentroidCoords__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(doom_interfaces__msg__CentroidCoords, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "u",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(doom_interfaces__msg__CentroidCoords, u),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "v",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(doom_interfaces__msg__CentroidCoords, v),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_members = {
  "doom_interfaces__msg",  // message namespace
  "CentroidCoords",  // message name
  3,  // number of fields
  sizeof(doom_interfaces__msg__CentroidCoords),
  false,  // has_any_key_member_
  doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_member_array,  // message members
  doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_init_function,  // function to initialize message memory (memory has to be allocated)
  doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_type_support_handle = {
  0,
  &doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_members,
  get_message_typesupport_handle_function,
  &doom_interfaces__msg__CentroidCoords__get_type_hash,
  &doom_interfaces__msg__CentroidCoords__get_type_description,
  &doom_interfaces__msg__CentroidCoords__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_doom_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, doom_interfaces, msg, CentroidCoords)() {
  doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_type_support_handle.typesupport_identifier) {
    doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &doom_interfaces__msg__CentroidCoords__rosidl_typesupport_introspection_c__CentroidCoords_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
