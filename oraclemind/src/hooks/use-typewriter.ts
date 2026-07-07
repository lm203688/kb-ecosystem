import { useState, useEffect } from 'react';

/**
 * 打字机效果Hook
 * @param text 要显示的完整文本
 * @param speed 每字符延迟ms（0=立即显示全文）
 */
export function useTypewriter(text: string, speed: number = 15): string {
  const [displayed, setDisplayed] = useState(speed === 0 ? text : '');

  useEffect(() => {
    if (speed === 0) {
      setDisplayed(text);
      return;
    }

    setDisplayed('');
    let i = 0;
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1));
        i++;
      } else {
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed]);

  return displayed;
}
