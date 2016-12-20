import React from 'react';
import NodeList from './NodeList.babel.js';
import cookies from '../../../../common/js/cookies';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import {updateSurveys} from './../redux/actions.babel.js';


class Survey extends React.Component {


    constructor(props) {
        super(props);

        this.updateTitle = this.updateTitle.bind(this);
        this.addLanguage = this.addLanguage.bind(this);
        this.updateDefault = this.updateDefault.bind(this);
        this.updateNodeList = this.updateNodeList.bind(this);
        this.showSubSurvey = this.showSubSurvey.bind(this);
        this.submit = this.submit.bind(this);

        this.state = {
            title: {},
            languages: ['English'],
            default_language: 'English',
            survey_type: 'public',
            nodes: [],
            isSubmitted: false
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        let update = false;
        if (JSON.stringify(this.props)!==JSON.stringify(nextProps)) {
            console.log('survey props changed', this.props, nextProps)
            update = true
        }
        if (JSON.stringify(this.state)!==JSON.stringify(nextState)) {
            console.log('survey state changed', this.state, nextState)
            update = true
        }
        return update;
    }

    // showSubSurvey(subsurvey){
    //     console.log('made it back to survey')
    //     this.setState({current: subsurvey}, function(){
    //         console.log('current updated', this.state.current)
    //     })
    // }


    updateTitle(language, event) {
        let newTitle = {};
        newTitle[language] = event.target.value;
        
        let titleObj = Object.assign({}, this.state.title, newTitle);
        this.setState({title: titleObj}, function() {
            console.log('updated title', this.state.title);
            let new_survey = {title: this.state.title, default_language: this.state.default_language}
            this.props.updateSurveys(new_survey, this.props.survey.id)
        })
    }

    updateDefault(event) {
        this.setState({default_language: event.target.value}, function(){
            console.log('set state: default language updated', this.state.default_language);
        });
    }

    addLanguage(language){
        console.log('being called!')
        let languageList = [];
        languageList = languageList.concat(this.state.languages);
        // possible add check for duplicate
        languageList.push(language);
        this.setState({languages: languageList}, function(){
            console.log('language added', language, this.state.languages);
        });
    }

    updateNodeList(nodelist) {
        console.log('update nodelist being called')
        console.log(this.state.current);
        console.log('this state nodes', this.state.nodes)
        // console.log('nodelist before', nodelist)
        // if (index < 0) nodelist.push(node)
        // else nodelist[index] = node;
        console.log('nodeList', nodelist);
        if (this.state.current) {
            console.log('IFFF CURRENT')
            let newCurrent = Object.assign({}, this.state.current, {nodes: nodelist})
            this.setState({current: newCurrent}, function(){
                console.log('lets see how this works....')
                console.log(this.state.current)
                console.log(this.state.nodes)
            })
        } else {
            console.log('before survey', this.state.nodes)
            let newnodes = [];
            newnodes = newnodes.concat(nodelist);
            this.setState({nodes: newnodes}, function(){
                console.log('nodes from survey', this.state.nodes);
            })
        }
    }

    submit() {
        // var survey2 = {
        //     title: {English: 'other responses'},
        //     default_language: 'English',
        //       survey_type: 'public',
        //       metadata: {},
        //       nodes: [{
        //         node: {
        //             type_constraint: 'integer',
        //             allow_multiple: true,
        //             allow_other: true,
        //             title: {'English': 'multiple responses'},
        //             hint: {'English': 'select more than one'}
        //         }
        //     }]
        // }
        // console.log(survey2)
        // this.props.submitToDatabase(survey2)
        console.log('being called?')
        // const newSurvey = function deleteExcessParams(this.props.survey)
        // console.log('before submitting', newSurvey);
        this.props.submitToDatabase();
    }

    // test() {
        // var modelSurvey = {
        //   title: {English: 'languages survey 12',
        //         German: 'languages survey 12'},
        //   default_language: 'English',
        //   languages: ['English', 'German'],
        //   survey_type: 'public',
        //   metadata: {},
        //   nodes: [{
        //       node: {
        //         languages: ['English', 'German'],
        //         title: {
        //             English: 'english test',
        //             German: 'german test'
        //         },
        //         hint: {
        //             English: 'e hint',
        //             German: 'g hint'
        //         },
        //         type_constraint: 'text',
        //         logic: {}
        //     },
        //     {
        //         node: {
        //             languages: ['English', 'German'],
        //             title: {
        //                 English: 'english test 2',
        //                 German: 'german test 2'
        //             },
        //             hint: {
        //                 English: 'e hint',
        //                 German: 'g hint'
        //             },
        //             type_constraint: 'facility',
        //             logic: {}
        //         }
        //     },
        //         node: {
        //             type_constraint: 'facility',
        //             allow_multiple: true,
        //             title: {'English': 'Facility'},
        //             hint: {'English': 'Select the facility from the list, or add a new one.'},
        //             logic: {
        //                 'slat': 40.477398,
        //                 'nlat': 40.91758,
        //                 'wlng': -74.259094,
        //                 'elng': -73.700165,
        //             }
        //         }
        //     }]
    //     };
    // }


    render() {
        console.log('rendering survey')
        console.log(this.props.survey)
        return (
            <div className="container">
            {(!this.state.current && this.props.survey) &&
                <div>
                <div className="col-lg-8 survey center-block">
                    <div className="survey-header header">
                        Create a Survey
                    </div>
                    <SurveyTitle 
                        updateTitle={this.updateTitle}
                        languages={this.state.languages}
                    />
                    <hr/>
                    <Languages 
                        languages={this.state.languages}
                        addLanguage={this.addLanguage}
                        updateDefault={this.updateDefault}
                    />
                    <NodeList
                        key={this.props.survey_id}
                        submitted={this.props.submitted}
                        survey_id={this.props.survey.id}
                        submitting={this.state.isSubmitted}
                        survey_nodes={this.props.survey.nodes}
                        default_language={this.state.default_language}
                        updateNodeList={this.updateNodeList}
                        languages={this.state.languages}
                        showSubSurvey={this.showSubSurvey}
                    />
                </div>
                <button onClick={this.submit}>submit</button>
                </div>
            }
        </div>
    )
}
}


function SurveyTitle(props) {

    const languages = props.languages;

    function titleList(languages){
        return props.languages.map(function(language){
            return (
                <div className="col-xs-12 survey-title" key={language}>
                    <div className="language-text"><span className="language-header">{language}</span></div>
                    <textarea id="survey-title" className="form-control survey-title-text" rows="1"
                        onBlur={props.updateTitle.bind(null, language)}/>
                </div>
            )
        })
    }

        return (
            <div>
                <div className="form-group row survey-group">
                    <label htmlFor="survey-title" className="col-xs-4 col-form-label survey-label">Survey Title: </label>
                    {titleList()}
                </div>
            </div>
        )
}


function Languages(props){

    const languages = props.languages;

    function languageList(languages){
        return props.languages.map(function(language){
            console.log('language???', language)
            return (
                <option key={language} value={language}>{language}</option>
            )
        })
    }

    function languageHandler(event) {
        if (!event.target.value.length) return;
        console.log('handling', event.target.value)
        const newLang = event.target.value;
        event.target.value = '';
        props.addLanguage(newLang);
    }

    return (
        <div>
            <div className="form-group row survey-group">
                <label htmlFor="survey-title" className="col-xs-4 col-form-label survey-label">Languages: </label>
                <div className="col-xs-12">
                    Add Language: <input type="text" onBlur={languageHandler}/>
                    Default Language:
                        <select onChange={props.updateDefault}>
                            {languageList()}
                        </select>
                </div>
            </div>
        </div>
    )
}

function mapStateToProps(state){
    return {
        surveys: state.surveys
    };
}

function mapDispatchToProps(dispatch){
    return (
        bindActionCreators({updateSurveys: updateSurveys}, dispatch)
    )
}

export default connect(mapStateToProps, mapDispatchToProps)(Survey);

// export default Survey;
