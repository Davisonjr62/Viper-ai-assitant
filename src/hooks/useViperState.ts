import { useEffect, useState } from 'react';
import { ViperStateMachine } from '../core/ViperStateMachine';
import type { ViperState } from '../core/types';

export function useViperState() {
  const [s, setS] = useState<ViperState>(ViperStateMachine.getState());
  useEffect(() => {
    const unsubscribe = ViperStateMachine.subscribe((n) => setS(n));
    return unsubscribe;
  }, []);
  return s;
}
