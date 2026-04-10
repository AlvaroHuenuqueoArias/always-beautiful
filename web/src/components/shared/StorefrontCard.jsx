export default function StorefrontCard({
    eyebrow,
    title,
    description,
    meta,
    highlight = "camel",
    className = "",
    children
}) {
    const metaItems = Array.isArray(meta) ? meta : meta ? [meta] : [];

    return (
        <article
            className={[
                "storefront-card",
                `storefront-card--${highlight}`,
                className
            ]
                .filter(Boolean)
                .join(" ")}
        >
            {eyebrow ? (
                <p className="storefront-card__eyebrow">{eyebrow}</p>
            ) : null}

            {title ? <h3 className="storefront-card__title">{title}</h3> : null}

            {description ? (
                <p className="storefront-card__description">{description}</p>
            ) : null}

            {metaItems.length > 0 ? (
                <div className="storefront-card__meta">
                    {metaItems.map((item) => (
                        <span key={item} className="storefront-card__pill">
                            {item}
                        </span>
                    ))}
                </div>
            ) : null}

            {children ? <div className="storefront-card__body">{children}</div> : null}
        </article>
    );
}