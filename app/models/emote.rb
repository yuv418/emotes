class Emote < ApplicationRecord
  belongs_to :namespace
  has_one_attached :image, dependent: :destroy
  has_many_attached :resized_images, dependent: :destroy

  validates :image, :slug, :name, :emote_type, presence: true
  validates_uniqueness_of :slug, scope: :namespace
end
