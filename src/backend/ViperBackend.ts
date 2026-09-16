import { viperEventBus } from '../core/ViperEventBus';
import { classifyLocalCommand } from './LocalCommandRouter';

export const viperBackend = {
  connect() {},
  disconnect() {},
  async handleCommand(text: string) {
    viperEventBus.emit('COMMAND_RECEIVED', { text });
    const c = classifyLocalCommand(text);
    viperEventBus.emit('COMMAND_CLASSIFIED', c);
    if (!c.handled) {
      viperEventBus.emit('AI_TASK_STARTED', { text });
      return { path: 'ai', command: c } as const;
    }
    viperEventBus.emit('FAST_COMMAND_STARTED', c);
    try {
      if (!window.viperNative?.executeFastCommand) throw new Error('Native Viper command bridge is unavailable');
      const execution = window.viperNative.executeFastCommand(c.intent, c.entity);
      execution.then(()=>viperEventBus.emit('FAST_COMMAND_COMPLETED',c)).catch(error=>viperEventBus.emit('ERROR',{error}));
      return { path: 'local', command: c } as const;
    } catch (error) {
      viperEventBus.emit('ERROR', { error });
      return { path: 'error', error } as const;
    }
  },
};
