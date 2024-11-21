

var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

dagfuncs.rowSpan = function (params) {
    var Ref = params.data ? params.data.Reference : undefined;

    if (Ref !== '') {
        // have selected in column ref of height of 2*lenth rows
        return 10;
        
    } else {
        // all other rows should be just normal
        return 0;
    }
}



// var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

// dagcomponentfuncs.DCC_GraphClickData = function (props) {
//     const {setData} = props;
//     function setProps() {
//         const graphProps = arguments[0];
//         if (graphProps['clickData']) {
//             setData(graphProps);
//         }
//     }
//     return React.createElement(window.dash_core_components.Graph, {
//         figure: props.value,
//         setProps,
//         style: {height: '100%'},
//         config: {displayModeBar: false},
//     });
// };

var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.DCC_GraphClickData = function (props) {
    const { setData, value } = props;
    
    // Check if the value is a figure (you may need to adjust this condition)
    const isFigure = typeof value === 'object' && value.hasOwnProperty('data') && value.hasOwnProperty('layout');
    
    // If it's a figure, render the graph; otherwise, render the cell value
    if (isFigure) {
        return React.createElement(window.dash_core_components.Graph, {
            figure: value,
            setProps: (graphProps) => {
                if (graphProps['clickData']) {
                    setData(graphProps);
                }
            },
            style: { height: '100%' },
            config: { displayModeBar: false, scrollZoom : false},
        });
    } else {
        return String(value);
    }
};




// dagcomponentfuncs.CustomTooltip = function (props) {
//     info = [
//         React.createElement('h4', {}, "Certainty of evidence:"+ props.data.Certainty),
//         React.createElement('div', { style: { marginBottom: 8 } }, ''),
//         React.createElement('div', {}, 'Risk of bias: Not serious'),
//         React.createElement('div', {}, 'Inconsistency: Not serious'),
//         React.createElement('div', {}, 'Publication Bias: Not serious'),
//         React.createElement('div', {}, 'Imprecision:: Not serious'),
//         React.createElement('div', {}, 'Intransitivity: Not serious'),
//     ];
//     return React.createElement(
//         'div',
//         {
//             style: {
//                 border: '1pt solid white',
//                 backgroundColor: props.color || 'grey',
//                 padding: 10,
//                 lineHeight: '20px' 
//             },
//         },
//         info
//     );
// };
dagcomponentfuncs.CustomTooltip = function (props) {
    const certainty = props.data.Certainty;
    const withinstudy = props.data.within_study;
    const reporting = props.data.reporting;
    const indirectness = props.data.indirectness;
    const imprecision = props.data.imprecision;
    const heterogeneity = props.data.heterogeneity;
    const incoherence = props.data.incoherence;


    const backgroundColor = getBackgroundColorForCertainty(certainty);

    const info = [
        React.createElement('h4', {}, "Certainty of evidence: " + certainty),
        React.createElement('div', { style: { marginBottom: 8 } }, ''),
        React.createElement('div', {}, 'Within-study bias: '+ withinstudy),
        React.createElement('div', {}, 'Reporting bias: '+reporting),
        React.createElement('div', {}, 'Indirectness: '+indirectness),
        React.createElement('div', {}, 'Imprecision: '+imprecision),
        React.createElement('div', {}, 'Heterogeneity: '+heterogeneity),
        React.createElement('div', {}, 'Incoherence: '+incoherence),

    ];

    return React.createElement(
        'div',
        {
            style: {
                border: '1pt solid white',
                backgroundColor: backgroundColor,
                padding: 10,
                lineHeight: '20px',
            },
        },
        info
    );
};

function getBackgroundColorForCertainty(certainty) {
    switch (certainty) {
        case 'Low':
            return '#B85042';
        case 'Moderate':
            return 'rgb(248, 212, 157)';
        case 'High':
            return 'rgb(90, 164, 105)';
        default:
            return 'lightgrey'; // Default background color
    }
};



dagcomponentfuncs.CustomTooltip2 = function (props) {
    const certainty = props.data.Certainty_out1;
    const withinstudy = props.data.within_study_out1;
    const reporting = props.data.reporting_out1;
    const indirectness = props.data.indirectness_out1;
    const imprecision = props.data.imprecision_out1;
    const heterogeneity = props.data.heterogeneity_out1;
    const incoherence = props.data.incoherence_out1;


    const backgroundColor = getBackgroundColorForCertainty(certainty);

    const info = [
        React.createElement('h4', {}, "Certainty of evidence: " + certainty),
        React.createElement('div', { style: { marginBottom: 8 } }, ''),
        React.createElement('div', {}, 'Within-study bias: '+ withinstudy),
        React.createElement('div', {}, 'Reporting bias: '+reporting),
        React.createElement('div', {}, 'Indirectness: '+indirectness),
        React.createElement('div', {}, 'Imprecision: '+imprecision),
        React.createElement('div', {}, 'Heterogeneity: '+heterogeneity),
        React.createElement('div', {}, 'Incoherence: '+incoherence),

    ];

    return React.createElement(
        'div',
        {
            style: {
                border: '1pt solid white',
                backgroundColor: backgroundColor,
                padding: 10,
                lineHeight: '20px',
            },
        },
        info
    );
};


dagcomponentfuncs.CustomTooltip3 = function (props) {
    const certainty = props.data.Certainty_out2;
    const withinstudy = props.data.within_study_out2;
    const reporting = props.data.reporting_out2;
    const indirectness = props.data.indirectness_out2;
    const imprecision = props.data.imprecision_out2;
    const heterogeneity = props.data.heterogeneity_out2;
    const incoherence = props.data.incoherence_out2;


    const backgroundColor = getBackgroundColorForCertainty(certainty);

    const info = [
        React.createElement('h4', {}, "Certainty of evidence: " + certainty),
        React.createElement('div', { style: { marginBottom: 8 } }, ''),
        React.createElement('div', {}, 'Within-study bias: '+ withinstudy),
        React.createElement('div', {}, 'Reporting bias: '+reporting),
        React.createElement('div', {}, 'Indirectness: '+indirectness),
        React.createElement('div', {}, 'Imprecision: '+imprecision),
        React.createElement('div', {}, 'Heterogeneity: '+heterogeneity),
        React.createElement('div', {}, 'Incoherence: '+incoherence),

    ];

    return React.createElement(
        'div',
        {
            style: {
                border: '1pt solid white',
                backgroundColor: backgroundColor,
                padding: 10,
                lineHeight: '20px',
            },
        },
        info
    );
};





function getBackgroundColorForCertainty(certainty) {
    switch (certainty) {
        case 'Low':
            return '#B85042';
        case 'Moderate':
            return 'rgb(248, 212, 157)';
        case 'High':
            return 'rgb(90, 164, 105)';
        default:
            return 'lightgrey'; // Default background color
    }
};






dagcomponentfuncs.DMC_Button = function (props) {
    const { setData, data } = props;

    function onClick() {   
        
        const temp = data.Treatment;
        props.node.setDataValue( "Treatment", data.Reference);
        props.node.setDataValue( "Reference", temp);
        
        // const tempRR = data.RR;
        props.node.setDataValue("RR", parseFloat((1 / data.RR).toFixed(2)))
        props.node.setDataValue("RR_out2", parseFloat((1 / data.RR_out2).toFixed(2)));

        // const temp3 = data.RR_out2;
        // props.node.setDataValue("RR_out2", data.RR_inv2);
        // props.node.setDataValue("RR_inv2", temp3);

        setData();
    }

    // Create the icon element
    let icon;
    if (props.icon) {
        icon = React.createElement(window.dash_iconify.DashIconify, {
            icon: props.icon,
            style: {
                color: props.color, // Apply color directly to the icon
                fontSize: '24px' // Adjust size as needed
            },
        });
    }

    // Return a minimal button with no background or borders
    return React.createElement(
        "div", // Change from a button to a div or span for no button appearance
        {
            onClick,
            style: {
                background: 'none',   // No background
                border: 'none',       // No border
                cursor: 'pointer',    // Pointer cursor for clickability
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
            },
        },
        icon // Use only the icon as content
    );
};

