export default function SectionHeading({
    eyebrow,
    title,
    description,
    align = "left"
}) {
    return (
        <div className={`section-heading section-heading--${align}`}>
            {eyebrow ? <p className="section-heading__eyebrow">{eyebrow}</p> : null}
            {title ? <h2 className="section-heading__title">{title}</h2> : null}
            {description ? (
                <p className="section-heading__description">{description}</p>
            ) : null}
        </div>
    );
}