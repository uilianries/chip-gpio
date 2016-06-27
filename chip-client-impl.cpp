/**
 * \file
 * \brief CHIP client implementation
 */

#include "chip-client-impl.hpp"

namespace chip {
namespace gpio {

ClientImpl::ClientImpl(unsigned pin)
{
    // TODO
    (void)pin;
}

ClientImpl::~ClientImpl()
{
    // TODO
}

bool ClientImpl::mode(Direction direction)
{
    // TODO
    return false;
}

bool ClientImpl::write(Level level)
{
    // TODO
    return false;
}

Level ClientImpl::read()
{
    // TODO
    return Level::low;
}

bool ClientImpl::enable()
{
    // TODO
    return false;
}

bool ClientImpl::disable()
{
    // TODO
    return false;
}

Client::Ptr Client::create(unsigned pin)
{
    Client::Ptr client;

    return client;
}

}  // namespace gpio
}  // namespace chip
