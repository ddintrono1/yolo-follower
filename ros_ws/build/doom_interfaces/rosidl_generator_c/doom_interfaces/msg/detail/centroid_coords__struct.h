// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from doom_interfaces:msg/CentroidCoords.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "doom_interfaces/msg/centroid_coords.h"


#ifndef DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__STRUCT_H_
#define DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/CentroidCoords in the package doom_interfaces.
/**
  * This custom message interface is used to publish the 
  * bounding box centroid pixel coordinates.
 */
typedef struct doom_interfaces__msg__CentroidCoords
{
  std_msgs__msg__Header header;
  int16_t u;
  int16_t v;
} doom_interfaces__msg__CentroidCoords;

// Struct for a sequence of doom_interfaces__msg__CentroidCoords.
typedef struct doom_interfaces__msg__CentroidCoords__Sequence
{
  doom_interfaces__msg__CentroidCoords * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} doom_interfaces__msg__CentroidCoords__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__STRUCT_H_
