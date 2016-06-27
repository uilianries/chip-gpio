/**
 * \file
 * \brief CHIP GPIO Client
 */
#ifndef CHIP_GPIO_CLIENT_HPP_
#define CHIP_GPIO_CLIENT_HPP_

#include <memory>

namespace chip {
namespace gpio {

/**
 * \brief Direction mode
 */
enum class Direction { input, output };

/**
 * \brief GPIO level
 */
enum class Level { high, low };

/**
 * \brief Ask command to GPIO Server
 */
class Client {
   public:
    using Ptr = std::unique_ptr<Client>;

    Client(const Client&) = delete;
    Client& operator=(const Client&) = delete;
    Client(Client&&) = delete;
    Client& operator=(Client&&) = delete;

    virtual ~Client() = default;

    /**
     * \brief Create new client instance
     * \param pin Board pin
     */
    Ptr create(unsigned pin);

    /**
     * \brief Set direction mode
     */
    virtual bool mode(Direction direction) = 0;

    /**
     * \brief Write level on GPIO
     */
    virtual bool write(Level level) = 0;

    /**
     * \brief Read current level on GPIO
     */
    virtual Level read() = 0;

   protected:
    /**
     * \brief Enable GPIO
     */
    virtual bool enable() = 0;

    /**
     * \brief Disable GPIO
     */
    virtual bool disable() = 0;

    Client() = default;
};

}  // namespace gpio
}  // namespace chip

#endif  // CHIP_GPIO_CLIENT_HPP_
