module.exports = (feature) => {
    const props = feature.properties;

    props.id = feature.id;

    props.name = `${props.first_name} ${props.last_name}`;

    props.roles = JSON.parse(props.roles);

    if (props.country !== '') {
        props.country = JSON.parse(props.country);
    }

    props.city = props.city.trim();
    props.state = props.state.trim();

    props.languages = JSON.parse(props.languages);

    return props;
};
