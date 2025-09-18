// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from doom_interfaces:msg/CentroidCoords.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "doom_interfaces/msg/centroid_coords.hpp"


#ifndef DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__BUILDER_HPP_
#define DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "doom_interfaces/msg/detail/centroid_coords__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace doom_interfaces
{

namespace msg
{

namespace builder
{

class Init_CentroidCoords_v
{
public:
  explicit Init_CentroidCoords_v(::doom_interfaces::msg::CentroidCoords & msg)
  : msg_(msg)
  {}
  ::doom_interfaces::msg::CentroidCoords v(::doom_interfaces::msg::CentroidCoords::_v_type arg)
  {
    msg_.v = std::move(arg);
    return std::move(msg_);
  }

private:
  ::doom_interfaces::msg::CentroidCoords msg_;
};

class Init_CentroidCoords_u
{
public:
  explicit Init_CentroidCoords_u(::doom_interfaces::msg::CentroidCoords & msg)
  : msg_(msg)
  {}
  Init_CentroidCoords_v u(::doom_interfaces::msg::CentroidCoords::_u_type arg)
  {
    msg_.u = std::move(arg);
    return Init_CentroidCoords_v(msg_);
  }

private:
  ::doom_interfaces::msg::CentroidCoords msg_;
};

class Init_CentroidCoords_header
{
public:
  Init_CentroidCoords_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CentroidCoords_u header(::doom_interfaces::msg::CentroidCoords::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_CentroidCoords_u(msg_);
  }

private:
  ::doom_interfaces::msg::CentroidCoords msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::doom_interfaces::msg::CentroidCoords>()
{
  return doom_interfaces::msg::builder::Init_CentroidCoords_header();
}

}  // namespace doom_interfaces

#endif  // DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__BUILDER_HPP_
