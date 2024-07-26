"use client";
import { useState } from "react";
import { default as NextImage, ImageProps } from "next/image";
import cn from "classnames";

const Image = ({ className, ...props }: ImageProps) => {
    const [loaded, setLoaded] = useState(false);

    return (
        <NextImage
            className={`inline-block align-top opacity-0 transition-opacity ${
                loaded && "opacity-100"
            } ${className}`}
            onLoad={(e) => setLoaded(true)}
            {...props}
        />
    );
};

export default Image;
