import React from "react";
import ReactDOM from "react-dom";
import ProductSlideshowFromHtml from "./ProductSlideshowFromHtml";
import ProductPageButtons from "./ProductPageButtons";
import { getChildOrError } from "./util";
import "./styles.css";
 
function renderIfExists(comp, elemId) {
    const node = document.getElementById(elemId);
    if (node) {
        ReactDOM.render(comp, node);
    }
}

renderIfExists(<ProductSlideshowFromHtml />, "ProductPage-slideshow");

const nodes = document.getElementsByClassName("ProductPage-buttons");
for (let node of nodes) {
    ReactDOM.render(
        <ProductPageButtons
            stock={Number(getChildOrError(node, "ProductPage-stock").innerText)}
            initialQuantity={Number(getChildOrError(node, "ProductPage-quantity").innerText)}
            downBtn={getChildOrError(node, "ProductPage-quantity-down").outerHTML}
            upBtn={getChildOrError(node, "ProductPage-quantity-up").outerHTML}
            />,
        node
    );
}