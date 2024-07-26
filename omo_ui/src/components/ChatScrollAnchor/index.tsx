import React, { useRef, useEffect } from 'react';
import { useInView } from 'react-intersection-observer';

interface ChatScrollAnchorProps {
  trackVisibility?: boolean;
}

export function ChatScrollAnchor({ trackVisibility }: ChatScrollAnchorProps) {
  const { ref, entry, inView } = useInView({
      trackVisibility,
      delay: 100,
      rootMargin: '0px 0px -50px 0px',
  });

  useEffect(() => {
      if (trackVisibility && !inView) {
        console.log('scrolling')
          entry?.target.scrollIntoView({
              block: 'start',
              behavior: 'smooth',
          });
      }
  }, [inView, entry, trackVisibility]);

  return <div ref={ref} className="h-px w-full"></div>;
}
