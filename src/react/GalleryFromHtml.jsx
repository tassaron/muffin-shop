/* This component gets the product information from the page HTML
 * and creates the Gallery component (a slideshow with filmstrip of thumbnails).
 */
import { Component } from "react"
import { getNodeOrError } from "../../static/js/util.js";
import ImageGallery from 'react-image-gallery';

class GalleryFromHtml extends Component {
    constructor() {
        super();

        // Get `productName`
        const nameNode = getNodeOrError("ProductPage-name");
        // Get `slideImages`
        const slidesNode = getNodeOrError("ProductPage-slides");
        const items = slidesNode.innerHTML.split(",");
        this.slideImages = items.map((item) => {
            return {
                original: item,
                thumbnail: item,
                originalAlt: nameNode.innerHTML,
                thumbnailAlt: nameNode.innerHTML,
                description: nameNode.innerHTML
            }
        });
        slidesNode.innerHTML = "";
    }

    render() {
        return (
            <div>
                <ImageGallery items={this.slideImages} />
            </div>
        );
    }
}

export default GalleryFromHtml;
