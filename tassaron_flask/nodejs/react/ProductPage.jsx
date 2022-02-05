/* This component gets the product information from the page HTML
 * and composes the Product Page out of other components.
*/
import React, { Component } from "react";
import ProductSlideshow from "./ProductSlideshow";


class ProductPage extends Component {
    constructor() {
        super();

        const getNodeOrError = function(name) {
            const node = document.getElementById(name);
            if (!node) {
                throw new ReferenceError(`Missing DOM node with ID ${name}`);
            }
            return node
        }

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

export default ProductPage