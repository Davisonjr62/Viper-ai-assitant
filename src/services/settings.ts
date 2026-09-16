import { DEFAULT_SETTINGS, type ViperSettings } from '../core/types';

export const settingsService = {
  async load(): Promise<ViperSettings> {
    if (window.viperNative) {
      return { ...DEFAULT_SETTINGS, ...await window.viperNative.getSettings() };
    }

    try {
      return {
        ...DEFAULT_SETTINGS,
        ...JSON.parse(localStorage.getItem('viper-settings') || '{}'),
      };
    } catch {
      return DEFAULT_SETTINGS;
    }
  },

  onChanged(_cb: (p: Partial<ViperSettings>) => void) {
    return () => {};
  },
};
