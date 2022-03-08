/* This component gets the product information from the page HTML
 * and creates the Gallery component (a slideshow with filmstrip of thumbnails).
 */
import React, { Component } from "react"
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
        this.node = React.createRef();

        // https://github.com/xiaolin/react-image-gallery#props
        this.slideImages = items.map((item) => {
            return {
                original: item,
                thumbnail: item,
                originalAlt: nameNode.innerHTML,
                thumbnailAlt: nameNode.innerHTML,
                description: nameNode.innerHTML,
            }
        });
        slidesNode.innerHTML = "";
        this.fullScreen = false;
    }

    getSlideElement(index) {
        return this.node.current.imageGallery.current.childNodes[0].childNodes[0].childNodes[2].childNodes[0].childNodes[index].childNodes[0];
    }

    toggleFullscreen(fullscreen) {
        this.fullscreen = fullscreen;
        const image = this.getSlideElement(this.node.current.getCurrentIndex());
        if (fullscreen) {
            image.setAttribute("style", "height: 90vh");
        } else {
            image.setAttribute("style", "height: calc(50vh)");
        }
    }

    slideTo(index) {
        let image = this.getSlideElement(this.node.current.getCurrentIndex());
        image.setAttribute("style", "height: calc(50vh)");
        if (this.fullscreen) {
            image = this.getSlideElement(index);
            image.setAttribute("style", "height: 90vh")
        }
    }

    render() {
        return (
            <div>
                <ImageGallery
                    ref={this.node}
                    items={this.slideImages}
                    onScreenChange={(fullscreen) => this.toggleFullscreen(fullscreen)}
                    onBeforeSlide={(index) => this.slideTo(index)}
                />
            </div>
        );
    }
}

export default GalleryFromHtml;