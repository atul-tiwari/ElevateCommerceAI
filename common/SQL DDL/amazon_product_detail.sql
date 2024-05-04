-- ElevateCommerceAI.amazon_product_details definition

CREATE TABLE `amazon_product_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `asin` varchar(100) DEFAULT NULL,
  `title` varchar(1000) DEFAULT NULL,
  `link` varchar(100) DEFAULT NULL,
  `categories_flat` varchar(100) DEFAULT NULL,
  `rating` decimal(10,0) DEFAULT NULL,
  `ratings_total` int DEFAULT NULL,
  `feature_bullets` text,
  `attributes` text,
  `specifications` text,
  `bestsellers_rank` text,
  `brand` varchar(100) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;