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
        //const nameNode = getNodeOrError("ProductPage-name");
        // Get `slideImages`
        const slidesNode = getNodeOrError("ProductPage-slides");
        let items = slidesNode.innerHTML.split("\"\"\",");
        items = items.map((item) => item.trim().substring(3));
        items[items.length-1] = items[items.length-1].substring(0, items[items.length-1].length - 3);
        slidesNode.innerHTML = "";
        const images = [];
        const titles = [];
        for (let i = 0; i < items.length; i++) {
            if (i % 2 == 0) {
                images.push(items[i]);
            } else {
                titles.push(items[i]);
            }
        }
        this.fullScreen = false;
        this.node = React.createRef();

        // https://github.com/xiaolin/react-image-gallery#props
        let slides = images.map((item) => {
            return {
                original: item,
                thumbnail: item,
            }
        });
        for (let i = 0; i < images.length; i++) {
            if (!titles[i]) continue;
            slides[i] = {
                ...slides[i],
                originalAlt: titles[i],
                thumbnailAlt: titles[i],
                description: titles[i],
            }
        }
        this.slideImages = slides;
    }

    getSlideElement(index) {
        if (this.slideImages.length > 1) {
            return this.node.current.imageGallery.current.childNodes[0].childNodes[0].childNodes[2].childNodes[0].childNodes[index].childNodes[0];
        }
        return this.node.current.imageGallery.current.childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes[index];
    }

    toggleFullscreen(fullscreen) {
        this.fullscreen = fullscreen;
        const image = this.getSlideElement(this.node.current.getCurrentIndex());
        if (fullscreen) {
            image.setAttribute("style", "height: 90vh");
        } else {
            image.setAttribute("style", "height: var(--gallery-image-height)");
        }
    }

    slideTo(index) {
        let image = this.getSlideElement(this.node.current.getCurrentIndex());
        image.setAttribute("style", "height: var(--gallery-image-height)");
        if (this.fullscreen) {
            image = this.getSlideElement(index);
            image.setAttribute("style", "height: 90vh")
        }
    }

    render() {
        return (
            <div>
            {this.slideImages.length > 1 ? (
                    <ImageGallery
                        ref={this.node}
                        items={this.slideImages}
                        onScreenChange={(fullscreen) => this.toggleFullscreen(fullscreen)}
                        onBeforeSlide={(index) => this.slideTo(index)}
                        showPlayButton={false}
                    />
                ) : (
                    <img src={this.slideImages[0].original} alt={this.slideImages[0].originalAlt} className="center-cropped w-100" />
                )
            }
            </div>
        );
    }
}

export default GalleryFromHtml;
