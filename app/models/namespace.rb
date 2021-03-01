class Namespace < ApplicationRecord
  has_and_belongs_to_many :user
  has_many :emotes, dependent: :destroy
  validates :slug, presence: true, uniqueness: true
  before_destroy :prevent_global_delete,  prepend: true # Too bad we can't verify before a delete
  # We don't need to bother validating whether the namespace is global, as the safe params prevents creating a global namespace.

  def prevent_global_delete
    if global
      errors.add(:base, :cannot_delete_global)
      throw :abort
   end
  end
end
