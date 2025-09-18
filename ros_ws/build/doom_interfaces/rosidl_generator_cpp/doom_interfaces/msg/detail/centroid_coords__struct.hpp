// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from doom_interfaces:msg/CentroidCoords.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "doom_interfaces/msg/centroid_coords.hpp"


#ifndef DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__STRUCT_HPP_
#define DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__doom_interfaces__msg__CentroidCoords __attribute__((deprecated))
#else
# define DEPRECATED__doom_interfaces__msg__CentroidCoords __declspec(deprecated)
#endif

namespace doom_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CentroidCoords_
{
  using Type = CentroidCoords_<ContainerAllocator>;

  explicit CentroidCoords_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->u = 0;
      this->v = 0;
    }
  }

  explicit CentroidCoords_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->u = 0;
      this->v = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _u_type =
    int16_t;
  _u_type u;
  using _v_type =
    int16_t;
  _v_type v;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__u(
    const int16_t & _arg)
  {
    this->u = _arg;
    return *this;
  }
  Type & set__v(
    const int16_t & _arg)
  {
    this->v = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    doom_interfaces::msg::CentroidCoords_<ContainerAllocator> *;
  using ConstRawPtr =
    const doom_interfaces::msg::CentroidCoords_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      doom_interfaces::msg::CentroidCoords_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      doom_interfaces::msg::CentroidCoords_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__doom_interfaces__msg__CentroidCoords
    std::shared_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__doom_interfaces__msg__CentroidCoords
    std::shared_ptr<doom_interfaces::msg::CentroidCoords_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CentroidCoords_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->u != other.u) {
      return false;
    }
    if (this->v != other.v) {
      return false;
    }
    return true;
  }
  bool operator!=(const CentroidCoords_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CentroidCoords_

// alias to use template instance with default allocator
using CentroidCoords =
  doom_interfaces::msg::CentroidCoords_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace doom_interfaces

#endif  // DOOM_INTERFACES__MSG__DETAIL__CENTROID_COORDS__STRUCT_HPP_
