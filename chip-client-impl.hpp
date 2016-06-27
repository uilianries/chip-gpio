/**
 * \file
 * \brief CHIP GPIO Client implementation
 */
#ifndef CHIP_GPIO_CLIENT_IMPL_HPP_
#define CHIP_GPIO_CLIENT_IMPL_HPP_

#include "chip-client.hpp"

namespace chip {
namespace gpio {

class ClientImpl : public Client {
   public:
    /**
     * \brief Create Client instance
     * \param pin Board pin
     */
    ClientImpl(unsigned pin);

    /**
     * \brief Finish GPIO connection
     */
    ~ClientImpl();

    /**
     * \brief Set direction mode
     */
    bool mode(Direction direction) override;

    /**
     * \brief Write level on GPIO
     */
    bool write(Level level) override;

    /**
     * \brief Read level on GPIO
     */
    Level read() override;

   protected:
    /**
     * \brief Enable GPIO
     */
    bool enable() override;

    /**
     * \brief Disable GPIO
     */
    bool disable() override;
};

}  // namespace gpio
}  // namespace chip

#endif  // CHIP_GPIO_CLIENT_IMPL_HPP_
