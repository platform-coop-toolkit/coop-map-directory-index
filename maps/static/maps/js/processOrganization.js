module.exports = (feature) => {
    const props = feature.properties;

    props.id = feature.id;

    props.type = (props.type === 'null') ? null : props.type;

    if (props.country !== '') {
        props.country = JSON.parse(props.country);
    }

    props.city = props.city.trim();
    props.state = props.state.trim();

    props.categories = JSON.parse(props.categories);
    props.languages = JSON.parse(props.languages);
    props.sectors = JSON.parse(props.sectors);
    props.socialnetworks = JSON.parse(props.socialnetworks);
    props.tools = JSON.parse(props.tools);

    return props;
};
