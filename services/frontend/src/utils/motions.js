export const motionButtonGlow = {
  initial: {
    "box-shadow": "0 0 1px rgba(0, 0, 0, 0)",
  },
  enter: {
    "box-shadow": "0 0 5px rgba(99, 226, 183, 1)",
    transition: {
      duration: 2000,
      repeat: Infinity,
      ease: "easeInOut",
      repeatType: "mirror",
    },
  },
};

export const motionShakeX = (index) => {
  return {
    initial: {
      x: 0,
    },
    enter: {
      x: 20,
      transition: {
        delay: index * 75,
        duration: 2000,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "mirror",
      },
    },
  };
};

export const motionShakeY = (index) => {
  return {
    initial: {
      y: 0,
    },
    enter: {
      y: 20,
      transition: {
        delay: index * 70,
        duration: 2000,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "mirror",
      },
    },
  };
};

import { useMotion } from "@vueuse/motion";

export function initialMotion(ref, index, onCompleteVariant = "levitateY") {
  const { variant, ...args } = useMotion(ref, {
    initial: {
      y: 100,
      opacity: 0,
    },
    enter: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 350,
        damping: 20,
        delay: index * 50,
        onComplete: () => {
          variant.value = onCompleteVariant;
        },
      },
    },
    levitateY: {
      y: 20,
      rotateX: 15,
      transition: {
        duration: 2000,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "mirror",
      },
    },
    levitateX: {
      x: 15,
      rotateY: 15,
      transition: {
        duration: 2000,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "mirror",
      },
    },
  });
  return { ...args };
}

const levitateX = (ref, index) => {
  const { variant } = useMotion(ref, {
    initial: {
      y: 100,
      opacity: 0,
    },
    enter: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 350,
        damping: 20,
        delay: index * 50,
        onComplete: () => {
          variant.value = "levitate";
        },
      },
    },
    levitate: {
      x: 25,
      transition: {
        duration: 2000,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "mirror",
      },
    },
  });
};

export function getMotion(key) {
  let map = { levitateX };
  return map[key];
}
