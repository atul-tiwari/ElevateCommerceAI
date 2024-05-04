-- ElevateCommerceAI.amazon_image_links definition

CREATE TABLE `amazon_image_links` (
  `id` int NOT NULL AUTO_INCREMENT,
  `asin` varchar(100) DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `link` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;