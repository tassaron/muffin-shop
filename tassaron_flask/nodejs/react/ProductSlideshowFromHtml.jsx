/* This component gets the product information from the page HTML
 * and creates the Product Slideshow.
*/
import React, { Component } from "react";
import ProductSlideshow from "./ProductSlideshow";
import getNodeOrError from "./util";


class ProductSlideshowFromHtml extends Component {
    constructor() {
        super();

        // Get `productName`
        const nameNode = getNodeOrError("ProductPage-name");
        this.productName = nameNode.innerHTML;
        // Get `slideImages`
        const slidesNode = getNodeOrError("ProductPage-slides");
        this.slideImages = slidesNode.innerHTML.split(",");
        slidesNode.innerHTML = "";
    }

    render() {
        return (
            <div>
                <ProductSlideshow slideImages={this.slideImages} productName={this.productName} />
            </div>
        )
    }
}

export default ProductSlideshowFromHtml