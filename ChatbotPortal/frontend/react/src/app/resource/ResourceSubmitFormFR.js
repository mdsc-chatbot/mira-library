/**
 * @file: ResourceSubmitFormFrench.js
 * @summary: Composant permettant à l'utilisateur de soumettre une ressource (version française)
 * @author: Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen
 * @licence: MIT
 */

import React, { Component } from "react";
import axios from "axios";
import { Slider } from "react-semantic-ui-range";
import { Container, Form, Header, Input, Message, Icon, Popup, Checkbox, Divider, Dropdown, Dimmer, Segment, Image, Loader, Button } from "semantic-ui-react";
import TagDropdown from "./TagDropdown";
import TitleDropdown from "./TitleDropdown";
import OrganizationNameDropdown from "./OrganizationNameDropdown";
import CategoryDropdown from './CategoryDropdown';
import HoursOfOperationWidget from "./HoursOfOperationWidget";
import ResourceTypeDropdown from './ResourceTypeDropdown';
import ResourceFormatDropdown from './ResourceFormatDropdown';
import { SecurityContext } from '../contexts/SecurityContext';
import * as styles from "./ResourceSubmitForm.css";
import { Link, withRouter } from "react-router-dom";

class ResourceSubmitFormFR extends Component {
    static contextType = SecurityContext;

    constructor(props) {
        super(props);
        this.state = {
            dimmerLoading: false,
            timeZone:"-6 UTC",
            resourceTypeRelateTextnumber: false,
            resourceTypeRelateEmail: false,
            resourceTypeRelatePhonenumber: false,
            resourceTypeRelateAddress: false,
            ageArray: [0, 110],
            resourceId: null,
            title: "",
            catText: "",
            tagInitValue: "",
            definition: "",
            resourceTypeIsInformative: false,
            organization_name: "",
            url: "",
            general_url: "",
            rating: 5,
            attachment: null,
            attachmentPath: "",
            comments: "",
            description: "",
            organization_description: "",
            email: "",
            phone_numbers: "",
            text_numbers: "",
            physical_address: "",
            resource_type: "SR",
            errors: {},
            tags: [],
            url_validated: true,
            currentTags: null,
            submitted: 0,
            alwaysAvailable: true,
            hourBools: [
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
                [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
            ],
            allTimeZones: [ {key:"-12 UTC",value:"-12 UTC",text:"-12 UTC"},
            {key:"-11 UTC",value:"-11 UTC",text:"-11 UTC"},
            {key:"-10 UTC",value:"-10 UTC",text:"-10 UTC"},
            {key:"-9:30 UTC",value:"-9:30 UTC",text:"-9:30 UTC"},
            {key:"-9 UTC",value:"-9 UTC",text:"-9 UTC"},
            {key:"-8 UTC",value:"-8 UTC",text:"-8 UTC"},
            {key:"-7 UTC",value:"-7 UTC",text:"-7 UTC"},
            {key:"-6 UTC",value:"-6 UTC",text:"-6 UTC"},
            {key:"-5 UTC",value:"-5 UTC",text:"-5 UTC"},
            {key:"-4 UTC",value:"-4 UTC",text:"-4 UTC"},
            {key:"-3 UTC",value:"-3 UTC",text:"-3 UTC"},
            {key:"-3:30 UTC",value:"-3:30 UTC",text:"-3:30 UTC"},
            {key:"-2 UTC",value:"-2 UTC",text:"-2 UTC"},
            {key:"-1 UTC",value:"-1 UTC",text:"-1 UTC"},
            {key:"0 UTC",value:"0 UTC",text:"0 UTC"},
            {key:"+1 UTC",value:"+1 UTC",text:"+1 UTC"},
            {key:"+2 UTC",value:"+2 UTC",text:"+2 UTC"},
            {key:"+3 UTC",value:"+3 UTC",text:"+3 UTC"},
            {key:"+3:30 UTC",value:"+3:30 UTC",text:"+3:30 UTC"},
            {key:"+4 UTC",value:"+4 UTC",text:"+4 UTC"},
            {key:"+4:30 UTC",value:"+4:30 UTC",text:"+4:30 UTC"},
            {key:"+5 UTC",value:"+5 UTC",text:"+5 UTC"},
            {key:"+5:30 UTC",value:"+5:30 UTC",text:"+5:30 UTC"},
            {key:"+5:45 UTC",value:"+5:45 UTC",text:"+5:45 UTC"},
            {key:"+6 UTC",value:"+6 UTC",text:"+6 UTC"},
            {key:"+6:30 UTC",value:"+6:30 UTC",text:"+6:30 UTC"},
            {key:"+7 UTC",value:"+7 UTC",text:"+7 UTC"},
            {key:"+8 UTC",value:"+8 UTC",text:"+8 UTC"},
            {key:"+8:45 UTC",value:"+8:45 UTC",text:"+8:45 UTC"},
            {key:"+9 UTC",value:"+9 UTC",text:"+9 UTC"},
            {key:"+9:30 UTC",value:"+9:30 UTC",text:"+9:30 UTC"},
            {key:"+10 UTC",value:"+10 UTC",text:"+10 UTC"},
            {key:"+10:30 UTC",value:"+10:30 UTC",text:"+10:30 UTC"},
            {key:"+11 UTC",value:"+11 UTC",text:"+11 UTC"},
            {key:"+12 UTC",value:"+12 UTC",text:"+12 UTC"},
            {key:"+12:45 UTC",value:"+12:45 UTC",text:"+12:45 UTC"},
            {key:"+13 UTC",value:"+13 UTC",text:"+13 UTC"},
            {key:"+14 UTC",value:"+14 UTC",text:"+14 UTC"},
            ]
        };
        this.baseState = this.state;
    }

    componentDidMount() {
        //check if resource id is in url to know if we come to form for editing the resource or not
        const resourceId = this.props.location.search ? this.props.location.search.substring(4) : '';
        if (!this.context.security.is_logged_in) console.log('not logged in')
        console.log(resourceId)
        if (resourceId != '' && this.context.security.is_logged_in) this.get_resource_details(resourceId);
        
        // Debug: Log the French tag categories we're using
        console.log('French form loaded with tag categories:', [
            'Type de ressource',
            'Coûts', 
            'Problème de santé',
            'Langue',
            'Public'
        ]);
    }

    get_resource_details = (resourceID) => {
        // Having the permission header loaded
        const options = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.context.security.token}`
        };
        axios
            .get(`/chatbotportal/resource/retrieve/${resourceID}/`, { headers: options })
            .then(res => {
                console.log('I got resources', res.data)
                if (res.data.definition) {
                    this.setState({ resourceTypeIsInformative: true });
                } else {
                    this.setState({ resourceTypeIsInformative: false });
                }
                this.setState({ resource_type: res.data.resource_type });
                this.setState({ title: res.data.title });
                this.setState({ timeZone: res.data.time_zone });
                this.setState({ definition: res.data.definition });
                this.setState({ organization_name: res.data.organization_name });
                this.setState({ url: res.data.url });
                this.setState({ general_url: res.data.general_url });
                this.setState({ rating: res.data.rating });
                this.setState({ comments: res.data.comments });
                this.setState({ description: res.data.description });
                this.setState({ created_by_user: res.data.created_by_user });
                this.setState({ created_by_user_pk: res.data.created_by_user_pk });
                this.setState({ organization_description: res.data.organization_description });

                if(res.data.email!=null && res.data.email!=""){ 
                    this.setState({ resourceTypeRelateEmail: true });
                    this.setState({ email: res.data.email });
                }

                if(res.data.phone_numbers!=null && res.data.phone_numbers!=""){
                    this.setState({ resourceTypeRelatePhonenumber: true });
                    this.setState({ phone_numbers: res.data.phone_numbers });
                }

                if(res.data.text_numbers!=null && res.data.text_numbers!=""){ 
                    this.setState({ resourceTypeRelateTextnumber: true });
                    this.setState({ text_numbers: res.data.text_numbers });
                }

                if(res.data.physical_address!=null && res.data.physical_address!=""){
                    this.setState({ resourceTypeRelateAddress: true });
                    this.setState({ physical_address: res.data.physical_address });
                }

                this.setState({ tagInitValue: res.data.tags });
                this.setState({ hours_of_operation: res.data.hours_of_operation });
                this.setState({ ageArray: [res.data.min_age, res.data.max_age] });
                if (res.data.hours_of_operation != null && res.data.hours_of_operation != "MON:;TUE:;WED:;THU:;FRI:;SAT:;SUN:;") {
                    this.setState({ alwaysAvailable: false });
                    this.decodeHours(res.data.hours_of_operation);
                }
                // let submit btn know we are in edit mode
                this.setState({ resourceId: resourceID });
            });
    };

    decodeHours = (hoursFromDB) => {
        console.log('hoursFromDB', hoursFromDB);
        var weekIndex;
        var newHourBools = this.state.hourBools;
        var dayArray = hoursFromDB.split(';');
        dayArray.forEach((day, index) => {
            if (day == '') {
                return;
            }
            switch (dayArray[index].substring(0, 3)) {
                case "MON":
                    weekIndex = 0
                    break;
                case "TUE":
                    weekIndex = 1
                    break;
                case "WED":
                    weekIndex = 2
                    break;
                case "THU":
                    weekIndex = 3
                    break;
                case "FRI":
                    weekIndex = 4
                    break;
                case "SAT":
                    weekIndex = 5
                    break;
                case "SUN":
                    weekIndex = 6
                    break;
            }
            const hourArray = day.substring(4).split(',');
            hourArray.forEach(hour => {
                if (hour == '') {
                    return;
                }
                newHourBools[weekIndex][hour - 1] = true;
            });
        });

        console.log('new bool', newHourBools);
        this.setState({ hourBools: newHourBools });
    }

    toggle = () => this.setState((prevState) => ({ alwaysAvailable: !prevState.alwaysAvailable }))

    render() {
        var dateTabs = null;
        if (!this.state.alwaysAvailable) {
            dateTabs = [
                <Dropdown selection value={"-6 UTC"} options={[{key:"-6 UTC",value:"-6 UTC",text:"-6 UTC"}]} />, // Simplified for demo
                // <HoursOfOperationWidget hourBools={this.state.hourBools} />
            ];
        }

        return (
            <Container style={{ paddingTop: "3%", paddingLeft: "10%", paddingRight: "10%", paddingBottom: "3%" }}>
                <Header as="h3" color="blue">Soumission de ressource (Français)</Header>
                <Form>
                    <Form.Field>
                        <label>Titre de la ressource/Resource Title <Popup content="(Format: [nom de l'organisation][type de ressource] - Exemple: Services de crise Canada Ligne téléphonique)" trigger={<Icon name='question circle' />} /></label>
                        <Input
                            required
                            name="title"
                            placeholder="Entrez le titre de la ressource"
                        />
                    </Form.Field>
                    <Form.Field>
                        <label>Nom de l'organisation/Organization Name <Popup content="(Exemple: Services de crise Canada)" trigger={<Icon name='question circle' />} /></label>
                        <Input
                            required
                            name="organization_name"
                            placeholder="Entrez le nom de l'organisation"
                        />
                    </Form.Field>
                    <Form.Field>
                        <label>Description de l'organisation/Organization Description</label>
                        <Form.TextArea
                            required
                            name="organization_description"
                            placeholder="Entrez une brève description de l'organisation"
                            rows={2}
                        />
                    </Form.Field>
                    <Form.Field>
                        <label>Description du service/Service Description</label>
                        <Form.TextArea
                            name="description"
                            placeholder="Entrez une brève description du service"
                            rows={2}
                        />
                    </Form.Field>
                    <Divider hidden />
                    <Form.Field>
                        <label>Type de ressource/Resource Type</label>
                        <TagDropdown
                            required
                            name="typeRessourceTags"
                            tagCat="Type de ressource"
                            value={this.state.tags}
                            onChange={tags => this.setState({ tags })}
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>URL de la ressource/Resource URL <Popup content="URL pointant vers l'endroit où la ressource a été obtenue. (Exemple: https://mdsc.ca/resources/56)" trigger={<Icon name='question circle' />} /> <Popup content="Ce champ est OPTIONNEL" trigger={<Icon name='flag' color='green' />} /></label>
                        <Input
                            name="url"
                            placeholder="https://exemple.com/ressource"
                        />
                    </Form.Field>
                    <Form.Field>
                        <label>URL de la page d'accueil/Homepage URL <Popup content="(Exemple: https://mdsc.ca)" trigger={<Icon name='question circle' />} /> <Popup content="Ce champ est OPTIONNEL" trigger={<Icon name='flag' color='green' />} /></label>
                        <Input
                            name="general_url"
                            placeholder="https://exemple.com"
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>Coûts/Costs</label>
                        <TagDropdown
                            name="coutsTags"
                            tagCat="Coûts"
                            value={this.state.tags}
                            onChange={tags => this.setState({ tags })}
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>Âge</label>
                    </Form.Field>
                    <Form.Group>
                        <Form.Input
                            inline
                            label="Min"
                            name="minAge"
                            width={2}
                            value={this.state.ageArray[0]}
                            placeholder="âge min"
                        />
                        <Form.Input
                            inline
                            name="maxAge"
                            label="Max"
                            width={2}
                            value={this.state.ageArray[1]}
                            placeholder="âge max"
                        />
                        <Form.Input
                            inline
                            width={12}
                            className="invisiblee"
                        />
                    </Form.Group>
                    <Divider hidden />

                    <Form.Field>
                        <label>Localisation(s)/Location(s) <Popup content="Localisations/régions pour les ressources physiques/pertinentes par localisation." trigger={<Icon name='question circle' />} /></label>
                        <Form.Group className={styles.dropdownPadding}>
                            <TagDropdown
                                required
                                name="locationTags"
                                tagCat="Location"
                                value={this.state.tags}
                                onChange={tags => this.setState({ tags })}
                            />
                        </Form.Group>
                    </Form.Field>

                    <Form.Field>
                        <label>Problème de santé/Health Problem(s) <Popup content="Tags pour tout problème de santé mentale que cette ressource aborde, définit, etc." trigger={<Icon name='question circle' />} /></label>
                        <TagDropdown
                            required
                            name="problemeSanteTags"
                            tagCat="Problème de santé"
                            value={this.state.tags}
                            onChange={tags => this.setState({ tags })}
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>Langue/Language <Popup content="Langues dans lesquelles cette ressource est écrite/disponible." trigger={<Icon name='question circle' />} /></label>
                        <TagDropdown
                            required
                            name="langueTags"
                            tagCat="Langue"
                            value={this.state.tags}
                            onChange={tags => this.setState({ tags })}
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>Public/Resource Audiences <Popup content="Si cette ressource a été créée pour soutenir les membres d'un groupe particulier (ex: LGBTQ2S+) ou d'une profession (ex: médecins, vétérans), veuillez ajouter le type de groupe ici" trigger={<Icon name='question circle' />} /> <Popup content="Ce champ est OPTIONNEL" trigger={<Icon name='flag' color='green' />} /></label>
                        <TagDropdown
                            name="publicTags"
                            tagCat="Public"
                            value={this.state.tags}
                            onChange={tags => this.setState({ tags })}
                        />
                    </Form.Field>
                    <Divider hidden />

                    <Form.Field>
                        <label>Autres/Tous les tags (optionnel)/Other/All Tags (optional) <Popup content="Pour tout ce qui pourrait ne pas entrer dans les autres catégories, comme les services fournis, les groupes de genre pertinents, les organisations, les groupes d'utilisateurs, etc." trigger={<Icon name='question circle' />} /> <Popup content="Ce champ est OPTIONNEL" trigger={<Icon name='flag' color='green' />} /></label>
                        <Form.Group className={styles.dropdownPadding}>
                            <TagDropdown
                                initValue={this.state.tagInitValue}
                                name="tags"
                                value={this.state.tags}
                                onChange={tags => this.setState({ tags })}
                            />
                        </Form.Group>
                    </Form.Field>

                    <Form.Field>
                        <label>Disponibilité de la ressource/Resource Availability <Popup content="Si la ressource n'est pas toujours disponible, décochez ceci et remplissez les heures ci-dessous." trigger={<Icon name='question circle' />} /></label>
                        <Checkbox
                            label='Ressource disponible 24/7'
                            onChange={this.toggle}
                            checked={this.state.alwaysAvailable}
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>Commentaires/Comments <Popup content="Ce champ est OPTIONNEL" trigger={<Icon name='flag' color='green' />} /></label>
                        <Form.TextArea
                            name="comments"
                            placeholder="Entrez des commentaires (optionnel)"
                            rows={2}
                        />
                    </Form.Field>

                    <Form.Field>
                        <label>Télécharger une pièce jointe/Upload an attachment <Popup content="Ce champ est OPTIONNEL" trigger={<Icon name='flag' color='green' />} /></label>
                        <Input
                            type="file"
                            name="attachment"
                        />
                    </Form.Field>
                    {dateTabs}
                    <Divider hidden />

                    <Form.Button name="submit" content="Soumettre" color="green" />
                </Form>
            </Container>
        );
    }
}

export default withRouter(ResourceSubmitFormFR);