import { Link } from "react-router-dom";

export default function StorefrontButton({
    to,
    children,
    variant = "primary",
    size = "md",
    className = "",
    type = "button",
    ...props
}) {
    const classes = [
        "storefront-button",
        `storefront-button--${variant}`,
        `storefront-button--${size}`,
        className
    ]
        .filter(Boolean)
        .join(" ");

    if (to) {
        return (
            <Link to={to} className={classes} {...props}>
                {children}
            </Link>
        );
    }

    return (
        <button type={type} className={classes} {...props}>
            {children}
        </button>
    );
}