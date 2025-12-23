#pragma once
#include <cstdint>
#include <iosfwd>

#include <functional>
#include <string>
#include <vector>


class CrossPointSettings {
 private:
  // Private constructor for singleton
  CrossPointSettings() = default;

  // Static instance
  static CrossPointSettings instance;

 public:
  // Delete copy constructor and assignment
  CrossPointSettings(const CrossPointSettings&) = delete;
  CrossPointSettings& operator=(const CrossPointSettings&) = delete;

  // Should match with SettingsActivity text
  enum SLEEP_SCREEN_MODE { DARK = 0, LIGHT = 1, CUSTOM = 2, COVER = 3 };

  // Sleep screen settings
  uint8_t sleepScreen = DARK;
  // Text rendering settings
  uint8_t extraParagraphSpacing = 1;
  // Duration of the power button press
  uint8_t shortPwrBtn = 0;

  ~CrossPointSettings() = default;

  // Get singleton instance
  static CrossPointSettings& getInstance() { return instance; }

  uint16_t getPowerButtonDuration() const { return shortPwrBtn ? 10 : 500; }

  bool saveToFile() const;
  bool loadFromFile();
};

enum class SettingType { TOGGLE, ENUM, ACTION };

struct SettingInfo {
  const char* name;                        // Display name of the setting
  SettingType type;                        // Type of setting
  uint8_t CrossPointSettings::* valuePtr;  // Pointer to member in CrossPointSettings (for TOGGLE/ENUM)
  std::vector<std::string> enumValues;
};

// Helper macro to access settings
#define SETTINGS CrossPointSettings::getInstance()

static const int settingsCount = 4;
static const SettingInfo settingsList[settingsCount] = {
    {"Sleep Screen", SettingType::ENUM, &CrossPointSettings::sleepScreen, {"Dark", "Light", "Custom", "Cover"}},
    {"Extra Paragraph Spacing", SettingType::TOGGLE, &CrossPointSettings::extraParagraphSpacing, {}},
    {"Short Power Button Click", SettingType::TOGGLE, &CrossPointSettings::shortPwrBtn, {}},
    {"Check for updates", SettingType::ACTION, nullptr, {}},
};
