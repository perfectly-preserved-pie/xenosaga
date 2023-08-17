dagcomponentfuncs.CustomTooltip = function (props) {
    var cellValue = props.value;  // Extract the cell's value

    return React.createElement(
        'div',
        {
            style: {
                border: '2pt solid white',
                backgroundColor: props.color || 'grey',
                padding: 10,
            },
        },
        cellValue  // Display the cell's value in the tooltip
    );
};
