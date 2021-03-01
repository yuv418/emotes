class Emote < ApplicationRecord
  belongs_to :namespace
  has_one_attached :image
  has_many_attaced :resized_images
end
