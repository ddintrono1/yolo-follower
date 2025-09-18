// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from doom_interfaces:msg/CentroidCoords.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "doom_interfaces/msg/centroid_coords.hpp"


#ifndef DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__TRAITS_HPP_
#define DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "doom_interfaces/msg/detail/centroid_coords__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace doom_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CentroidCoords & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: u
  {
    out << "u: ";
    rosidl_generator_traits::value_to_yaml(msg.u, out);
    out << ", ";
  }

  // member: v
  {
    out << "v: ";
    rosidl_generator_traits::value_to_yaml(msg.v, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CentroidCoords & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: u
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "u: ";
    rosidl_generator_traits::value_to_yaml(msg.u, out);
    out << "\n";
  }

  // member: v
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "v: ";
    rosidl_generator_traits::value_to_yaml(msg.v, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CentroidCoords & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace doom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use doom_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const doom_interfaces::msg::CentroidCoords & msg,
  std::ostream & out, size_t indentation = 0)
{
  doom_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use doom_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const doom_interfaces::msg::CentroidCoords & msg)
{
  return doom_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<doom_interfaces::msg::CentroidCoords>()
{
  return "doom_interfaces::msg::CentroidCoords";
}

template<>
inline const char * name<doom_interfaces::msg::CentroidCoords>()
{
  return "doom_interfaces/msg/CentroidCoords";
}

template<>
struct has_fixed_size<doom_interfaces::msg::CentroidCoords>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<doom_interfaces::msg::CentroidCoords>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<doom_interfaces::msg::CentroidCoords>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__TRAITS_HPP_
